class CreateMessages < ActiveRecord::Migration[6.0]
  def change
    create_table :messages do |t|
      t.integer :sender_id, null: false, foreign_key: { to_table: :users }
      t.integer :receiver_id, null: false, foreign_key: { to_table: :users }
      t.text :content, null: false
      t.string :status, default: 'sent'

      t.timestamps
    end

    add_index :messages, [ :sender_id, :receiver_id ]
    add_index :messages, :receiver_id
  end
end
