# frozen_string_literal: true

module Mutations
  class DeleteUserMutation < BaseMutation
    field :user, Types::UserType, null: true
    field :errors, [ String ], null: false

    argument :id, ID, required: true, description: "The ID of the user to be deleted."

    def resolve(id:)
      user = User.find_by(id: id)

      if user.nil?
        {
          user: nil,
          errors: [ "User not found" ]
        }
      else
        user.destroy
        {
          user: user,
          errors: []
        }
      end
    end
  end
end
