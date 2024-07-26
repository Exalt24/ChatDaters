module Mutations
  class LoginUser < BaseMutation
    argument :email, String, required: true

    field :token, String, null: true
    field :user, Types::UserType, null: true
    field :errors, [ String ], null: false

    def resolve(email:)
      user = User.find_by(email: email)

      if user
        # Generate a token for the user
        token = JsonWebToken.encode(user_id: user.id)
        { user: user, token: token, errors: [] }
      else
        # Return an error if the user is not found
        { user: nil, token: nil, errors: [ "Invalid email" ] }
      end
    end
  end
end
