class CreateConversations < ActiveRecord::Migration[6.0]
  def change
    create_table :conversations do |t|
      t.integer :user_ids, array: true, null: false, default: []
      t.integer :most_recent_message_id, foreign_key: { to_table: :messages }

      t.timestamps
    end

    add_index :conversations, :user_ids, using: 'gin'
    add_index :conversations, :most_recent_message_id
  end
end
