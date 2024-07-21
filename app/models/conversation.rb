class Conversation < ApplicationRecord
  # Associations
  has_many :messages, dependent: :destroy
  belongs_to :most_recent_message, class_name: "Message"

  # Validations
  validates :user_ids, presence: true, length: { minimum: 2 }

  # Scopes
  scope :between, ->(user1, user2) do
    where(user_ids: [ user1.id, user2.id ].sort)
  end
end
