require "uri"
require "base64"
require "cgi"

module Mutations
  class UpdateUserMutation < BaseMutation
    field :user, Types::UserType, null: false
    field :errors, [ String ], null: false

    argument :id, ID, required: true, description: "The ID of the user to be updated."
    argument :first_name, String, required: false
    argument :last_name, String, required: false
    argument :mobile_number, String, required: false
    argument :birthdate, GraphQL::Types::ISO8601Date, required: false
    argument :gender, String, required: false
    argument :sexual_orientation, String, required: false
    argument :gender_interest, String, required: false
    argument :location_country, String, required: false
    argument :location_region, String, required: false
    argument :location_city, String, required: false
    argument :school, String, required: false
    argument :bio, String, required: false
    argument :images, [ ApolloUploadServer::Upload ], required: false, description: "New image files to add."
    argument :deleted_images, [ String ], required: false, description: "URLs of images to delete."

    def resolve(id:, first_name: nil, last_name: nil, mobile_number: nil, birthdate: nil, gender: nil, sexual_orientation: nil, gender_interest: nil, location_country: nil, location_region: nil, location_city: nil, school: nil, bio: nil, images: [], deleted_images: [])
      user = User.find_by(id: id)
      Rails.logger.debug "Found user: #{user.inspect}"

      unless user
        return {
          user: nil,
          errors: [ "User not found" ]
        }
      end

      user.first_name = first_name if first_name.present?
      user.last_name = last_name if last_name.present?
      user.mobile_number = mobile_number if mobile_number.present?
      user.birthdate = birthdate if birthdate.present?
      user.gender = gender if gender.present?
      user.sexual_orientation = sexual_orientation if sexual_orientation.present?
      user.gender_interest = gender_interest if gender_interest.present?
      user.location_country = location_country if location_country.present?
      user.location_region = location_region if location_region.present?
      user.location_city = location_city if location_city.present?
      user.school = school if school.present?
      user.bio = bio if bio.present?

      Rails.logger.debug "User after updates: #{user.inspect}"

      # Handle deleting images
      if deleted_images.any?
        Rails.logger.debug "Deleting images: #{deleted_images.inspect}"
        handle_image_deletions(user, deleted_images)
      end

      # Handle adding new images
      if images.any?
        Rails.logger.debug "Uploading images: #{images.inspect}"
        handle_image_uploads(user, images)
      end

      if user.save
        Rails.logger.debug "User saved successfully"
        {
          user: user,
          errors: []
        }
      else
        Rails.logger.error "User save failed: #{user.errors.full_messages}"
        {
          user: nil,
          errors: user.errors.full_messages
        }
      end
    end

    private

    def handle_image_uploads(user, images)
      images.each do |image|
        # Attach each image to the user using Active Storage
        user.images.attach(io: image.tempfile,
                           filename: image.original_filename,
                           content_type: image.content_type)
         Rails.logger.debug "Attached image: #{image.original_filename}"
      end
    end

    def handle_image_deletions(user, deleted_image_urls)
      return unless deleted_image_urls.present?

      deleted_image_urls.each do |url|
        begin
          blob_id = extract_blob_id_from_url(url)
          next unless blob_id
          blob = ActiveStorage::Blob.find_by(id: blob_id)

          if blob
            attachment = user.images.find_by(blob_id: blob_id)
            attachment.purge if attachment
            Rails.logger.info "Deleted blob with id #{blob.id} from Active Storage."
          else
            Rails.logger.warn "Blob with id #{blob_id} not found in Active Storage."
          end
        rescue => e
          Rails.logger.error "Error deleting blob from Active Storage: #{e.message}"
        end
      end
    end

    def extract_blob_id_from_url(url)
      uri = URI.parse(url)
      encoded_segment = uri.path.split("/redirect/").last
      decoded_segment = CGI.unescape(encoded_segment)  # Use CGI.unescape to decode URL-encoded segment

      # Extract Base64-encoded JSON data
      base64_json_data = decoded_segment.split("--").first
      json_data = Base64.urlsafe_decode64(base64_json_data)
      blob_info = JSON.parse(json_data)
      blob_id = blob_info.dig("_rails", "data") if blob_info.is_a?(Hash) && blob_info.key?("_rails")
      Rails.logger.info "blob_id: #{blob_id}"
      blob_id
    rescue => e
      Rails.logger.error "Error extracting blob key from URL: #{e.message}"
      nil
    end
  end
end
