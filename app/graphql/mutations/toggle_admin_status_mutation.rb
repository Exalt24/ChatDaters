module Mutations
  class ToggleAdminStatusMutation < BaseMutation
    argument :id, ID, required: true

    field :user, Types::UserType, null: true
    field :errors, [ String ], null: false

    def resolve(id:)
      user = User.find_by(id: id)

      unless user
        return { user: nil, errors: [ "User not found" ] }
      end

      # Toggle admin status
      user.update(admin: !user.admin)

      if user.errors.any?
        { user: nil, errors: user.errors.full_messages }
      else
        { user: user, errors: [] }
      end
    end
  end
end
