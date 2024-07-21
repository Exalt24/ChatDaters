# frozen_string_literal: true

class GraphqlController < ApplicationController
  # Skip CSRF verification for the execute action
  skip_before_action :verify_authenticity_token, only: [ :execute ]

  before_action :authenticate_request, unless: -> { public_query_or_mutation? }

  def execute
    variables = prepare_variables(params[:variables])
    query = params[:query]
    operation_name = params[:operationName]

    # Extract files from params if they exist
    files = extract_files_from_params(params)

    # Add uploads to context for GraphQL execution
    context = {
      uploads: files,
      current_user: @current_user
      # You can add more context here if needed
      # current_user: current_user
    }

    result = GraphQlSchema.execute(query, variables: variables, context: context, operation_name: operation_name)
    render json: result
  rescue StandardError => e
    handle_error_in_development(e)
  end

  private

  # Prepare variables from params
  def prepare_variables(variables_param)
    case variables_param
    when String
      JSON.parse(variables_param) || {}
    when Hash
      variables_param
    when ActionController::Parameters
      variables_param.to_unsafe_hash
    else
      {}
    end
  end

  # Handle errors in development mode
  def handle_error_in_development(e)
    logger.error e.message
    logger.error e.backtrace.join("\n")

    render json: { errors: [ { message: e.message, backtrace: e.backtrace } ], data: {} }, status: 500
  end

  # Extract files from params if present (for Apollo Upload Server)
  def extract_files_from_params(params)
    return nil unless params[:operations] && params[:map]

    files_map = JSON.parse(params[:map])
    params[:operations] = JSON.parse(params[:operations])

    files = {}

    files_map.each do |key, value|
      indices = Array.wrap(value)  # Ensure value is an array
      indices.each do |index|
        files[key] ||= []
        files[key] << params.dig(:operations, key.to_sym, :variables, :files, index.to_i)
      end
    end

    files
  rescue JSON::ParserError => e
    raise StandardError, "Error parsing file upload parameters: #{e.message}"
  end

  def authenticate_request
    token = request.headers["Authorization"]&.split(" ")&.last
    return render json: { error: "Unauthorized" }, status: 401 unless token

    decoded_token = JsonWebToken.decode(token)
    Rails.logger.debug "Decoded Token: #{decoded_token}"

    user_id = decoded_token["user_id"]
    puts("USER: #{user_id}")
    @current_user = User.find_by(id: user_id)

    unless @current_user
      render json: { errors: [ "Not Authenticated" ] }, status: :unauthorized
    end
  rescue JWT::DecodeError => e
    Rails.logger.error "JWT Decode Error: #{e.message}"
    render json: { errors: [ "Invalid Token" ] }, status: :unauthorized
  rescue ActiveRecord::RecordNotFound => e
    Rails.logger.error "User Record Not Found: #{e.message}"
    render json: { errors: [ "User Not Found" ] }, status: :unauthorized
  rescue StandardError => e
    Rails.logger.error "Authentication Error: #{e.message}"
    render json: { errors: [ "Not Authenticated" ] }, status: :unauthorized
  end

  def public_query_or_mutation?
    public_operations = [ "CheckEmailExistence", "LoginUser", "CreateUser", "GetUsers", "LogoutUserMutation" ]
    public_operations.include?(params[:operationName])
  end
end
