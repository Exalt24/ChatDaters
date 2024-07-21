# frozen_string_literal: true

module Types
  class QueryType < Types::BaseObject
    field :node, Types::NodeType, null: true, description: "Fetches an object given its ID." do
      argument :id, ID, required: true, description: "ID of the object."
    end

    def node(id:)
      context.schema.object_from_id(id, context)
    end

    field :nodes, [ Types::NodeType, null: true ], null: true, description: "Fetches a list of objects given a list of IDs." do
      argument :ids, [ ID ], required: true, description: "IDs of the objects."
    end

    def nodes(ids:)
      ids.map { |id| context.schema.object_from_id(id, context) }
    end

    field :current_user, UserType do
      description "Fetches the current user"
    end

    def current_user
      context[:current_user]
    end

    field :user, UserType, null: false do
      description "Fetches a user by ID"
      argument :id, ID, required: true, description: "ID of the user"
    end

    def user(id:)
      User.find(id)  # Ensure it returns an array
    end

    field :check_user_existence, UserType, null: true do
      argument :id, ID, required: true
    end

    def check_user_existence(id:)
      User.find_by(id: id)
    end

    field :users, [ UserType ], null: false do
      description "All of the users"
    end

    def users
      User.all
    end

    field :check_email_existence, UserType, null: true do
      argument :email, String, required: true
    end

    def check_email_existence(email:)
      User.find_by(email: email)
    end

    field :isAdmin, Boolean, null: true do
      description "Check if a user is an admin"
      argument :id, ID, required: true, description: "ID of the user"
    end

    def isAdmin(id:)
      user = User.find_by(id: id)
      user&.admin
    end

    field :totalUsers, Integer, null: false do
      description "Fetches the total number of users"
    end

    def totalUsers
      User.where(admin: false).count
    end

    field :totalMatches, Integer, null: false do
      description "Fetches the total number of matches"
    end

    def totalMatches
      Match.where(status: "matched").count
    end

    field :matches, [ Types::MatchType ], null: false do
      description "Fetches all matches for the current user"
    end

    def matches
      user = context[:current_user]
      user ? user.matches.map { |match| match_for_user(user, match) } : []
    end

    field :conversation, ConversationType, null: false do
      description "Fetches a conversation by ID"
      argument :id, ID, required: true, description: "ID of the conversation"
    end

    def conversation(id:)
      Conversation.find(id)
    end

    private

      def match_for_user(user, match)
        {
          id: match.id,
          status: match.status,
          matched_user: match.matched_user
        }
      end
  end
end
