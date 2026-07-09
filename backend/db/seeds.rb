require 'faker'
require 'open-uri'

# Helper method to fetch an image from a URL
def fetch_image_from_url(url)
  io = URI.open(url)
  { io: io, filename: File.basename(URI.parse(url).path), content_type: 'image/jpeg' }
end

# Method to handle image uploads for a user
def handle_image_uploads(user, images)
  images.each do |image|
    user.images.attach(io: image[:io], filename: image[:filename], content_type: image[:content_type])
  end
end

# Method to create a user with specified attributes
def create_user(email, admin, gender, gender_interest, image_urls)
  user_attrs = {
    first_name: Faker::Name.first_name,
    last_name: Faker::Name.last_name,
    mobile_number: Faker::Base.regexify(/^(08|09)\d{9}$/),
    email: email,
    password: 'password',
    admin: admin,
    birthdate: Faker::Date.birthday(min_age: 18, max_age: 65).strftime('%Y-%m-%d'),
    gender: gender,  # Ensure this value matches the enum or valid options
    sexual_orientation: 'Straight',  # Ensure this value matches the enum or valid options
    gender_interest: gender_interest,
    location_country: Faker::Address.country,
    location_region: Faker::Address.state,
    location_city: Faker::Address.city,
    school: Faker::University.name,
    bio: Faker::Lorem.sentence,
    activated: true,
    images: image_urls.map { |url| fetch_image_from_url(url) }
  }

  # Initialize the user and handle image uploads
  user = User.new(user_attrs.except(:images))
  handle_image_uploads(user, user_attrs[:images])

  # Save the user
  if user.save
    Rails.logger.info("Created user with email #{user_attrs[:email]}")
  else
    Rails.logger.error("Failed to create user with email #{user_attrs[:email]}: #{user.errors.full_messages.join(', ')}")
  end
end

# List of image URLs
male_image_urls = [
  'https://randomuser.me/api/portraits/men/1.jpg',
  'https://randomuser.me/api/portraits/men/2.jpg',
  'https://randomuser.me/api/portraits/men/3.jpg',
  'https://randomuser.me/api/portraits/men/4.jpg',
  'https://randomuser.me/api/portraits/men/5.jpg'
]

female_image_urls = [
  'https://randomuser.me/api/portraits/women/1.jpg',
  'https://randomuser.me/api/portraits/women/2.jpg',
  'https://randomuser.me/api/portraits/women/3.jpg',
  'https://randomuser.me/api/portraits/women/4.jpg',
  'https://randomuser.me/api/portraits/women/5.jpg'
]

# Create initial users
create_user('admin1@gmail.com', true, 'Male', 'Female', male_image_urls)
create_user('user1@gmail.com', false, 'Female', 'Male', [ female_image_urls[0] ])
create_user('user2@gmail.com', false, 'Male', 'Female', male_image_urls)
create_user('user3@gmail.com', false, 'Female', 'Male', [ female_image_urls[2] ])

# Function to create multiple users
def create_multiple_users(number, male_image_urls, female_image_urls)
  number.times do |i|
    email = "user#{i + 4}@gmail.com"
    admin = false
    gender = i.even? ? 'Male' : 'Female'
    gender_interest = gender == 'Male' ? 'Female' : 'Male'
    image_urls = gender == 'Male' ? male_image_urls.sample(5) : female_image_urls.sample(1)

    create_user(email, admin, gender, gender_interest, image_urls)
  end
end

# Create 10 more users
create_multiple_users(10, male_image_urls, female_image_urls)

Rails.logger.info("Seeded additional 10 users with images.")
