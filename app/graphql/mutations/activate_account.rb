# app/graphql/mutations/activate_account.rb
module Mutations
  class ActivateAccount < BaseMutation
    argument :token, String, required: true
    argument :email, String, required: true

    field :user, Types::UserType, null: false
    field :errors, [ String ], null: false

    def resolve(token:, email:)
      user = User.find_by(email: email)
      if user && user.activation_token == token
        user.update(activated: true, activated_at: Time.zone.now)
        {
          user: user,
          errors: []
        }
      else
        {
          user: nil,
          errors: [ "Invalid token or email" ]
        }
      end
    end
  end
end
