require "jwt"

module JsonWebToken
  # Falls back to the app's own secret_key_base (SECRET_KEY_BASE env var, or the generated
  # tmp/local_secret.txt in development) when the encrypted credentials cannot be read.
  SECRET_KEY = Rails.application.credentials.secret_key_base || Rails.application.secret_key_base

  def self.encode(payload, exp = 24.hours.from_now)
    payload[:exp] = exp.to_i
    JWT.encode(payload, SECRET_KEY)
  end

  def self.decode(token)
    JWT.decode(token, SECRET_KEY)[0]
  rescue JWT::DecodeError => e
    Rails.logger.error "JWT Decode Error: #{e.message}"
    nil
  end
end
