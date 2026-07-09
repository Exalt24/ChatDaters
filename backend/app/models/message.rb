class Message < ApplicationRecord
  # Associations
  belongs_to :sender, class_name: "User"
  belongs_to :receiver, class_name: "User"
  belongs_to :conversation

  # Validations
  validates :sender_id, presence: true
  validates :receiver_id, presence: true
  validates :content, presence: true
  validates :status, inclusion: { in: [ "sent", "initial" ] }

  # Scopes
  scope :between, ->(user1, user2) {
    joins(:conversation).where("(messages.sender_id = ? AND messages.receiver_id = ?) OR (messages.sender_id = ? AND messages.receiver_id = ?)", user1.id, user2.id, user2.id, user1.id)
  }
end
