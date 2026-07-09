class Match < ApplicationRecord
  validates :user_ids, length: { is: 2 }
  validates :status, inclusion: { in: [ "pending", "matched" ] }

  scope :initiated_by, ->(user_id) { where("user_initiated = ?", user_id) }
  scope :received_by, ->(user_id) { where("user_received = ?", user_id) }
end
