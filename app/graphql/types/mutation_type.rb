# frozen_string_literal: true

module Types
  class MutationType < Types::BaseObject
    field :create_user_mutation, mutation: Mutations::CreateUserMutation
    field :update_user_mutation, mutation: Mutations::UpdateUserMutation
    field :delete_user_mutation, mutation: Mutations::DeleteUserMutation
    field :toggle_admin_status_mutation, mutation: Mutations::ToggleAdminStatusMutation
    field :login_user_mutation, mutation: Mutations::LoginUserMutation
    field :logout_user_mutation, mutation: Mutations::LogoutUserMutation
    field :match_user_mutation, mutation: Mutations::MatchUserMutation
    field :start_conversation_mutation, mutation: Mutations::StartConversationMutation
  end
end
