class AddProfileFieldsToUsers < ActiveRecord::Migration[7.2]
  def change
    add_column :users, :birthdate, :date
    add_column :users, :gender, :string
    add_column :users, :sexual_orientation, :string
    add_column :users, :gender_interest, :string
    add_column :users, :location_country, :string
    add_column :users, :location_region, :string
    add_column :users, :location_city, :string
    add_column :users, :school, :string
    add_column :users, :bio, :text
  end
end
