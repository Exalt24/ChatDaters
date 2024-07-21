module Types
  class ConversationType < Types::BaseObject
    field :id, ID, null: false
    field :users, [ UserType ], null: false
    field :most_recent_message, MessageType, null: true
    field :messages, [ MessageType ], null: true
    field :created_at, GraphQL::Types::ISO8601DateTime, null: false
    field :updated_at, GraphQL::Types::ISO8601DateTime, null: false

    def users
      object.user_ids.map { |user_id| User.find(user_id) }
    end

    def most_recent_message
      object.most_recent_message
    end

    def messages
      object.messages
    end

    def created_at
      object.created_at.iso8601 # Assuming object is the instance of your User model
    end

    def updated_at
      object.updated_at.iso8601 # Assuming object is the instance of your User model
    end
  end
end
