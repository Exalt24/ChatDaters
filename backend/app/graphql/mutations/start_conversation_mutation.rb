module Mutations
  class StartConversationMutation < BaseMutation
    argument :receiver_id, ID, required: true
    argument :content, String, required: true

    field :conversation, Types::ConversationType, null: true
    field :message, Types::MessageType, null: true
    field :errors, [ String ], null: false

    def resolve(receiver_id:, content:)
      sender = context[:current_user]
      receiver = User.find_by(id: receiver_id)

      unless receiver
        return { conversation: nil, message: nil, errors: [ "Receiver not found" ] }
      end

      # Find or create the conversation
      conversation = Conversation.between(sender, receiver).first_or_create do |conv|
        conv.user_ids = [ sender.id.to_i, receiver.id.to_i ].sort

        # Create an initial most_recent_message object
        initial_message = Message.create(
          sender: sender,
          receiver: receiver,
          content: "", # Initially empty content
          status: "initial",
          conversation: conv
        )

        conv.update(most_recent_message: initial_message)
      end

      # Verify if the conversation was created or retrieved correctly
      unless conversation.persisted?
        return { conversation: nil, message: nil, errors: [ "Failed to create conversation" ] }
      end

      # Create the actual message
      message = Message.new(
        sender: sender,
        receiver: receiver,
        content: content,
        status: "sent",
        conversation: conversation
      )

      if message.save
        # Update the conversation with the actual most recent message
        conversation.update(most_recent_message: message)

        { conversation: conversation, message: message, errors: [] }
      else
        # Handle the case where the actual message fails to save
        { conversation: nil, message: nil, errors: message.errors.full_messages }
      end
    end
  end
end
