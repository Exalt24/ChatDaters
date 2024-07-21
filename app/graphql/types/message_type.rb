module Types
  class MessageType < Types::BaseObject
    field :id, ID, null: false
    field :sender, UserType, null: false
    field :receiver, UserType, null: false
    field :content, String, null: false
    field :status, String, null: false
    field :created_at, GraphQL::Types::ISO8601DateTime, null: false
    field :updated_at, GraphQL::Types::ISO8601DateTime, null: false

    def sender
      User.find_by(id: object.sender_id)
    end

    def receiver
      User.find_by(id: object.receiver_id)
    end

    def created_at
      object.created_at.iso8601 # Assuming object is the instance of your User model
    end

    def updated_at
      object.updated_at.iso8601 # Assuming object is the instance of your User model
    end
  end
end
