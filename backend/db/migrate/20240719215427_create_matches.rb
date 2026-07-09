class CreateMatches < ActiveRecord::Migration[6.0]
  def change
    create_table :matches do |t|
      t.integer :user_ids, array: true, null: false, default: []
      t.integer :user_initiated, null: false
      t.integer :user_received, null: false
      t.string :status, default: 'pending'

      t.timestamps
    end

    add_index :matches, :user_ids, using: 'gin'
  end
end
