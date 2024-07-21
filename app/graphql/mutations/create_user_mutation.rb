module Mutations
  class CreateUserMutation < BaseMutation
    argument :email, String, required: true
    argument :first_name, String, required: true
    argument :last_name, String, required: true
    argument :mobile_number, String, required: true
    argument :password, String, required: true
    argument :birthdate, GraphQL::Types::ISO8601Date, required: true
    argument :gender, String, required: true
    argument :sexual_orientation, String, required: true
    argument :gender_interest, String, required: true
    argument :location_country, String, required: true
    argument :location_region, String, required: true
    argument :location_city, String, required: true
    argument :school, String, required: false
    argument :bio, String, required: false
    argument :images, [ ApolloUploadServer::Upload ], required: false

    field :user, Types::UserType, null: true
    field :errors, [ String ], null: false

    def resolve(email:, first_name:, last_name:, mobile_number:, password:, birthdate:, gender:, sexual_orientation:, gender_interest:, location_country:, location_region:, location_city:, school: nil, bio:, images: [])
      user = User.new(
        email: email,
        first_name: first_name,
        last_name: last_name,
        mobile_number: mobile_number,
        password: password,
        birthdate: birthdate,
        gender: gender,
        sexual_orientation: sexual_orientation,
        gender_interest: gender_interest,
        location_country: location_country,
        location_region: location_region,
        location_city: location_city,
        school: school,
        bio: bio
      )

      if images.present?
        handle_image_uploads(user, images)
      end

      if user.save
        { user: user, errors: [] }
      else
        { user: nil, errors: user.errors.full_messages }
      end
    end

    private
    def handle_image_uploads(user, images)
      images.each do |image|
        user.images.attach(io: image.tempfile, filename: image.original_filename, content_type: image.content_type)
      end
    end
  end
end
