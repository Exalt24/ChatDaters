class AddDetailsToUsers < ActiveRecord::Migration[7.2]
  def change
    add_column :users, :first_name, :string
    add_column :users, :last_name, :string
    add_column :users, :mobile_number, :string
    add_column :users, :admin, :boolean, default: false
    add_column :users, :password_digest, :string
  end
end
