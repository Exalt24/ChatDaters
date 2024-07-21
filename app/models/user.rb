class User < ApplicationRecord
  has_many_attached :images
  has_secure_password

  has_many :matches, ->(user) {
    unscope(where: :user_id)
    .where("user_ids @> ARRAY[?]::integer[]", [ user.id ])
  }, dependent: :destroy

  has_many :conversations, ->(user) {
    unscope(where: :user_id)
    .where("user_ids @> ARRAY[?]::integer[]", [ user.id ])
  }, dependent: :destroy

  has_many :messages_sent, class_name: "Message", foreign_key: "sender_id", dependent: :destroy
  has_many :messages_received, class_name: "Message", foreign_key: "receiver_id", dependent: :destroy


  validates :first_name, :last_name, presence: true, length: { maximum: 25 }
  validates :email, presence: true, uniqueness: true, format: { with: /\A[\w+\-.]+@[a-z\d\-.]+[a-z\d\-]+\.[a-z]+\z/i }
  validates :mobile_number, presence: true, format: { with: /\A(08|09)[0-9]{9}\z/, message: "must be a valid Philippine mobile number starting with 0" }
  validates :birthdate, presence: true
  validates :gender, presence: true, inclusion: { in: [ "Male", "Female" ], message: "%{value} is not a valid gender" }
  validates :sexual_orientation, presence: true, inclusion: { in: [ "Straight", "Gay/Lesbian", "Bisexual", "Other" ], message: "%{value} is not a valid sexual orientation" }
  validates :gender_interest, presence: true, inclusion: { in: [ "Male", "Female", "Any" ], message: "%{value} is not a valid gender interest" }
  validates :location_country, presence: true
  validates :location_region, presence: true
  validates :location_city, presence: true
  validates :bio, length: { minimum: 10, maximum: 300 }, allow_nil: true
  validates :password, presence: true, length: { minimum: 6 }, allow_nil: true
  validate :validate_images

  def validate_images
    if images.attached?
      if images.count > 5
        errors.add(:images, "cannot have more than 5 images")
      end
    else
      errors.add(:images, "must have at least one image")
    end
  end
end
