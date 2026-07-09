module Mutations
  class SendActivationEmail < BaseMutation
    argument :email, String, required: true

    field :success, Boolean, null: false
    field :errors, [ String ], null: false

    def resolve(email:)
      user = User.find_by(email: email)
      if user
        user.generate_activation_token unless user.activation_token.present?
        user.save
        UserMailer.account_activation(user).deliver_now
        {
          success: true,
          errors: []
        }
      else
        {
          success: false,
          errors: [ "User not found" ]
        }
      end
    end
  end
end
