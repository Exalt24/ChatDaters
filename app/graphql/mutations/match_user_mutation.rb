module Mutations
  class MatchUserMutation < BaseMutation
    argument :matched_user_id, ID, required: true

    field :match, Types::MatchType, null: true
    field :errors, [ String ], null: false

    def resolve(matched_user_id:)
      user = context[:current_user]

      # Convert IDs to integers and sort them
      user_ids = [ user.id.to_i, matched_user_id.to_i ].sort

      # Create or find the match
      match = Match.find_or_initialize_by(user_ids: user_ids)

      if match.new_record?
        match.user_initiated = user.id
        match.user_received = matched_user_id
        match.status = "pending"
        match.save
      else
        # Update status if the match was previously pending
        match.update(status: "matched") if match.status == "pending"
      end

      { match: match, errors: match.errors.full_messages }
    end
  end
end
