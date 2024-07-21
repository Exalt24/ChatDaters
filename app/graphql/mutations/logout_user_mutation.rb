module Mutations
  class LogoutUserMutation < BaseMutation
    field :success, Boolean, null: true
    field :errors, [ String ], null: false

    def resolve
      # Implement logout logic here
      context[:current_user] = nil  # Clear current user session or token

      { success: true, errors: [] }
    rescue => e
      { success: false, errors: [ e.message ] }
    end
  end
end
