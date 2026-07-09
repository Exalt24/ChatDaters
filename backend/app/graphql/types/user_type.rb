module Types
  class UserType < Types::BaseObject
    implements Types::NodeType

    graphql_name "User"
    description "A user"

    field :id, ID, null: false, description: "The ID of the user"
    field :email, String, null: false, description: "The email of the user"
    field :first_name, String, null: true, description: "The first name of the user"
    field :last_name, String, null: true, description: "The last name of the user"
    field :mobile_number, String, null: true, description: "The mobile number of the user"
    field :birthdate, GraphQL::Types::ISO8601Date, null: true, description: "The birthdate of the user"
    field :gender, String, null: true, description: "The gender of the user"
    field :sexual_orientation, String, null: true, description: "The sexual orientation of the user"
    field :gender_interest, String, null: true, description: "The gender interest of the user"
    field :location_country, String, null: true, description: "The location of the user (Country, State/Region, City)"
    field :location_region, String, null: true, description: "The location of the user (Country, State/Region, City)"
    field :location_city, String, null: true, description: "The location of the user (Country, State/Region, City)"
    field :school, String, null: true, description: "The school of the user"
    field :bio, String, null: true, description: "The bio of the user"
    field :images, [ String ], null: true, description: "The URLs of the images attached to the user"
    field :admin, Boolean, null: true, description: "The presence of the administrative privilege of a user"
    field :activated, Boolean, null: true, description: "The activation status of the user's account"
    field :created_at, GraphQL::Types::ISO8601DateTime, null: false, description: "The date and time when the user was created"
    field :updated_at, GraphQL::Types::ISO8601DateTime, null: false, description: "The date and time when the user was last updated"
    field :matches, [ MatchType ], null: true, description: "The matches of the user"
    field :conversations, [ ConversationType ], null: true, description: "The conversations of the user"

    def matches
      object.matches
    end

    def activated
      object.activated
    end

    def conversations
      object.conversations
    end

    def first_name
      object.first_name
    end

    def last_name
      object.last_name
    end

    def mobile_number
      object.mobile_number
    end

    def birthdate
      object.birthdate.iso8601 if object.birthdate
    end

    def gender
      object.gender
    end

    def sexual_orientation
      object.sexual_orientation
    end

    def gender_interest
      object.gender_interest
    end

    def location_country
      object.location_country
    end

    def location_region
      object.location_region
    end

    def location_city
      object.location_city
    end

    def school
      object.school
    end

    def bio
      object.bio
    end

    def images
      object.images.map do |image|
        Rails.application.routes.url_helpers.rails_blob_url(image)
      end
    end

    def created_at
      object.created_at.iso8601 # Assuming object is the instance of your User model
    end

    def updated_at
      object.updated_at.iso8601 # Assuming object is the instance of your User model
    end
  end
end
