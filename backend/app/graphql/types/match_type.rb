module Types
  class MatchType < Types::BaseObject
    field :id, ID, null: false
    field :users, [ UserType ], null: false
    field :user_initiated, UserType, null: false
    field :user_received, UserType, null: false
    field :status, String, null: false
    field :created_at, GraphQL::Types::ISO8601DateTime, null: false
    field :updated_at, GraphQL::Types::ISO8601DateTime, null: false

    def users
      object.user_ids.map { |user_id| User.find(user_id) }
    end

    def user_initiated
      User.find(object.user_initiated)
    end

    def user_received
      User.find(object.user_received)
    end

    def created_at
      object.created_at.iso8601 # Assuming object is the instance of your User model
    end

    def updated_at
      object.updated_at.iso8601 # Assuming object is the instance of your User model
    end
  end
end
