<template>
  <div class="signup-container">
    <div class="signup">
      <h1>Sign Up</h1>
      <div v-if="errors.length" class="error-message">
        <ul>
          <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
      </div>
      <Form @submit="signup" v-slot="{ errors }" class="signup-form">
        
        <div class="form-group">
          <label for="email">Email</label>
          <Field name="email" v-model="email" type="email" placeholder="Email" required class="input-field"
            :rules="validateEmail" />
          <ErrorMessage name="email" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
        <label for="name">Name</label>
        <div class="name-fields">
          
          <div>
          <Field name="firstName" v-model="firstName" type="text" placeholder="First Name" required class="input-field"
            :rules="validateFirstName" />
          <ErrorMessage name="firstName" class="text-red-600 text-sm" />
        </div>
        <div>
          <Field name="lastName" v-model="lastName" type="text" placeholder="Last Name" required class="input-field"
            :rules="validateLastName" />
          <ErrorMessage name="lastName" class="text-red-600 text-sm" />
        </div>
        </div>
      </div>
       
        <div class="form-group">
          <label for="mobileNumber">Mobile Number</label>
          <Field name="mobileNumber" v-model="mobileNumber" type="tel" placeholder="Mobile Number" required
            class="input-field" :rules="validateMobileNumber" />
          <ErrorMessage name="mobileNumber" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <Field name="password" v-model="password" type="password" placeholder="Password" required class="input-field"
            :rules="validatePassword" />
          <ErrorMessage name="password" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <Field name="confirmPassword" v-model="confirmPassword" type="password" placeholder="Confirm Password"
            required class="input-field" :rules="validateConfirmPassword" />
          <ErrorMessage name="confirmPassword" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label for="birthdate">Birthdate</label>
          <Field name="birthdate" v-model="birthdate" type="date" required class="input-field" :rules="validateBirthdate" />
          <ErrorMessage name="birthdate" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
        <label for="gender">Gender</label>
        <Field name="gender" v-model="gender" as="select" class="input-field" :rules="validateGender">
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </Field>
        <ErrorMessage name="gender" class="text-red-600 text-sm" />
      </div>

      <div class="form-group">
  <label for="sexualOrientation">Sexual Orientation</label>
  <Field name="sexualOrientation" v-model="sexualOrientation" as="select" class="input-field" :rules="validateSexualOrientation">
    <option value="">Select Sexual Orientation</option>
    <option value="Straight">Straight</option>
    <option value="Gay/Lesbian">Gay/Lesbian</option>
    <option value="Bisexual">Bisexual</option>
    <option value="Other">Other</option>
  </Field>
  <ErrorMessage name="sexualOrientation" class="text-red-600 text-sm" />
</div>

<div class="form-group">
  <label for="genderInterest">Gender Interest</label>
  <Field name="genderInterest" v-model="genderInterest" as="select" class="input-field" :rules="validateGenderInterest">
    <option value="">Select Gender Interest</option>
    <option value="Male">Male</option>
    <option value="Female">Female</option>
    <option value="Any">Any</option>
  </Field>
  <ErrorMessage name="genderInterest" class="text-red-600 text-sm" />
</div>
<div class="form-group">
          <label for="location">Location</label>
          <div class="location-fields">
            <div>
              <Field name="locationCountry" v-model="locationCountry" as="select" class="input-field" @change="onCountryChange" :rules="validateLocationCountry">
        <option value="">Select Country</option>
        <option v-for="(country, index) in countries" :key="index" :value="country.name">{{ country.name }}</option>
      </Field>
              <ErrorMessage name="locationCountry" class="text-red-600 text-sm" />
            </div>
            <div>
              <Field name="locationRegion" v-model="locationRegion" as="select" class="input-field" @change="onRegionChange" :rules="validateLocationRegion">
        <option value="">Select Region/State</option>
        <option v-for="(state, index) in selectedCountryStates" :key="index" :value="state.name">{{ state.name }}</option>
      </Field>

              <ErrorMessage name="locationRegion" class="text-red-600 text-sm" />
            </div>
            <div>
              <Field name="locationCity" v-model="locationCity" as="select" class="input-field" :rules="validateLocationCity">
          <option value="">Select City</option>
          <option v-for="(city, index) in cities" :key="index" :value="city.name">{{ city.name }}</option>
        </Field>
            <ErrorMessage name="locationCity" class="text-red-600 text-sm" />
          </div>
          </div>
        </div>
        <div class="form-group">
          <label for="school">School</label>
          <Field name="school" v-model="school" type="text" placeholder="School" class="input-field"
            :rules="validateSchool" />
          <ErrorMessage name="school" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label for="bio">Bio</label>
          <Field name="bio" v-model="bio"as="textarea" rows="4" placeholder="Bio" class="input-field" :rules="validateBio" />
          <ErrorMessage name="bio" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label for="images">Images</label>
          <Field name="images" v-model="images" type="file" multiple @change="handleFileUpload"  :rules="validateImages"/>
          
          <ErrorMessage name="images" class="text-red-600 text-sm" />
        </div>

        <button type="submit" class="signup-button">Sign Up</button>
        
      </Form>
      <p class="mt-4 text-center text-sm text-black">
      Do you have an account? 
      <router-link to="/login" class="text-blue-500 hover:text-blue-800">Login</router-link>
    </p>
    </div>
    
  </div>
</template>

<script>
import { Field, ErrorMessage, Form } from 'vee-validate';
import gql from 'graphql-tag';

export default {
  name: 'Signup',
  components: {
    Field,
    ErrorMessage,
    Form,
  },
  data() {
    return {
      email: '',
      firstName: '',
      lastName: '',
      mobileNumber: '',
      password: '',
      confirmPassword: '',
      birthdate: '',
      gender: '',
      sexualOrientation: '',
      genderInterest: '',
      locationCountry: '',
      locationRegion: '',
      locationCity: '',
      school: '',
      bio: '',
      images: [],
      errors: [],
      countries: [],
      selectedCountryStates: [],
      cities: [],
    };
  },
  methods: {
    async signup() {
      // Clear previous errors
      this.errors = [];

      // Perform password matching validation
      if (this.password !== this.confirmPassword) {
        this.errors.push('Passwords do not match.');
        return;
      }

       // Create FormData to handle file uploads
       const formData = new FormData();
      formData.append('email', this.email);
      formData.append('firstName', this.firstName);
      formData.append('lastName', this.lastName);
      formData.append('mobileNumber', this.mobileNumber);
      formData.append('password', this.password);
      formData.append('birthdate', this.birthdate);
      formData.append('gender', this.gender);
      formData.append('sexualOrientation', this.sexualOrientation);
      formData.append('genderInterest', this.genderInterest);
      formData.append('locationCountry', this.locationCountry);
      formData.append('locationRegion', this.locationRegion);
      formData.append('locationCity', this.locationCity);
      formData.append('school', this.school);
      formData.append('bio', this.bio);

      this.images.forEach(image => {
        formData.append('images[]', image);
      });

      // GraphQL mutation to create user
      this.$apollo
        .mutate({
          mutation: gql`
            mutation CreateUser(
              $email: String!
              $firstName: String!
              $lastName: String!
              $mobileNumber: String!
              $password: String!
              $birthdate: ISO8601Date!
              $gender: String!
              $sexualOrientation: String!
              $genderInterest: String!
              $locationCountry: String!
              $locationRegion: String!
              $locationCity: String!
              $school: String
              $bio: String
              $images: [Upload!]
            ) {
              createUserMutation( input: {
                email: $email
                firstName: $firstName
                lastName: $lastName
                mobileNumber: $mobileNumber
                password: $password
                birthdate: $birthdate
                gender: $gender
                sexualOrientation: $sexualOrientation
                genderInterest: $genderInterest
                locationCountry: $locationCountry
                locationRegion: $locationRegion
                locationCity: $locationCity
                school: $school
                bio: $bio
                images: $images
              }) {
                user {
                  id
                  email
                }
                errors
              }
            }
          `,
          variables: {
            email: this.email,
            firstName: this.firstName,
            lastName: this.lastName,
            mobileNumber: this.mobileNumber,
            password: this.password,
            birthdate: this.birthdate,
            gender: this.gender,
            sexualOrientation: this.sexualOrientation,
            genderInterest: this.genderInterest,
            locationCountry: this.locationCountry,
            locationRegion: this.locationRegion,
            locationCity: this.locationCity,
            school: this.school,
            bio: this.bio,
            images: this.images,
          },
        })
        .then(({ data }) => {
          if (data.createUserMutation.errors.length) {
            this.errors = data.createUserMutation.errors;
          } else {
            this.login();
          }
        })
        .catch((error) => {
          console.error(error.message);
          this.errors.push('An error occurred while signing up.');
        });
    },
    async login() {
      this.errors = [];
      // GraphQL mutation to login user
      this.$apollo
        .mutate({
          mutation: gql`
            mutation SendActivationEmail($email: String!) {
              sendActivationEmail(input: { email: $email }) {
                success
                errors
              }
            }
          `,
          variables: {
            email: this.email,
          },
        })
        .then(({ data }) => {
          if (data.sendActivationEmail.errors.length) {
            this.errors = data.sendActivationEmail.errors;
          } else {
            this.$router.push({ 
                name: 'Home', 
                query: { successMessage: 'Successfully sent an activation email. Please check your inbox' }
            });
          }
        })
        .catch((error) => {
          console.error(error.message);
          this.errors.push('An error occurred while logging in.');
        });
    },
    async validateEmail(value) {
  if (!value) {
    return 'Email is required';
  }
  if (!/^[\w+\-.]+@[a-z\d\-.]+\.[a-z]+$/.test(value)) {
    return 'Invalid email format';
  }

  try {
    const { data, errors } = await this.$apollo.query({
      query: gql`
        query CheckEmailExistence($email: String!) {
          checkEmailExistence(email: $email) {
          id
          email
        }
        }
      `,
      variables: {
        email: value
      }
    });

    if (errors) {
      console.error('GraphQL Errors:', errors);
      return 'Error checking email existence';
    }

    if (data.checkEmailExistence) {
      return 'Email already exists'; // Email is already taken
    }

    return true; // Email is available
  } catch (error) {
    console.error('Error:', error);
    return error.message// Handle unexpected errors
  }
},
    validateFirstName(value) {
      if (!value) {
        return 'First Name is required';
      }
      return true;
    },
    validateLastName(value) {
      if (!value) {
        return 'Last Name is required';
      }
      return true;
    },
    validateMobileNumber(value) {
      if (!value) {
        return 'Mobile Number is required';
      }
      if (!/^(08|09)[0-9]{9}$/.test(value)) {
        return 'Invalid mobile number format';
      }
      return true;
    },
    validatePassword(value) {
  if (!value) {
    return 'Password is required';
  }
  if (value.length < 6) {
    return 'Password must be at least 6 characters';
  }
  // Add more complex password rules if needed
  return true;
},

validateConfirmPassword(value) {
  if (!value) {
    return 'Confirm Password is required';
  }
  if (value !== this.password) {
    return 'Passwords do not match';
  }
  return true;
},
validateBirthdate(value) {
  if (!value) {
    return 'Birthdate is required';
  }

  // Calculate minimum birthdate (18 years ago from today)
  const today = new Date();
  const minBirthdate = new Date(today.getFullYear() - 18, today.getMonth(), today.getDate());

  // Convert entered birthdate to Date object
  const selectedDate = new Date(value);

  // Compare selected date with minimum birthdate
  if (selectedDate > minBirthdate) {
    return 'You must be at least 18 years old';
  }

  return true;
},

    validateGender(value) {
      if (!value) {
        return 'Gender is required';
      }
      // Add specific gender validation if needed
      return true;
    },
    validateSexualOrientation(value) {
      if (!value) {
        return 'Sexual Orientation is required';
      }
      // Add specific validation for sexual orientation if needed
      return true;
    },
    validateGenderInterest(value) {
      if (!value) {
        return 'Gender Interest is required';
      }
      // Add specific validation for gender interest if needed
      return true;
    },
    validateLocationCountry(value) {

  if (!value) {
    return 'Country is required';
  }

  // Add additional validation logic if needed

  return true;
}, validateLocationRegion(value) {

if (!value) {
  return 'Region is required';
}

// Add additional validation logic if needed

return true;
},
validateLocationCity(value) {

if (!value) {
  return 'City is required';
}

// Add additional validation logic if needed

return true;
},
    validateSchool(value) {
      // Optional validation for school if needed
      return true;
    },
    validateBio(value) {
  // Optional validation for bio
  if (!value) {
    return 'Bio is required';
  }

  const minLength = 10;
  const maxLength = 300;

  if (value.length < minLength || value.length > maxLength) {
    return `Bio must be between ${minLength} and ${maxLength} characters`;
  }

  return true; // Bio is valid
},
validateImages() {
  if (this.images.length === 0) {
    return 'At least one image is required';
  }

  if (this.images.length > 5) {
    return 'A maximum of 5 images can be uploaded'
  }
  return true;
},
handleFileUpload(event) {
  const files = event.target.files;
  this.images = Array.from(files); // Ensure this.images is properly assigned
},
async fetchCountriesAndStates() {
  try {
    const response = await fetch('https://countriesnow.space/api/v0.1/countries/states');
    const data = await response.json();
    if (!data.error) {
      // Extract countries and states from the API response
      this.countries = data.data.map(country => ({
        name: country.name,
        states: country.states.length > 0 ? country.states.map(state => ({
          name: state.name
        })) : [{ name: 'N/A' }]
      }));
    } else {
      console.error('Failed to fetch countries and states:', data.msg);
      // Handle error scenario
    }
  } catch (error) {
    console.error('Error fetching countries and states:', error.message);
    // Handle fetch error
  }
},  async fetchCities() {
      try {
        console.log("Fetching")
        if (this.locationCountry && this.locationRegion) {
          const response = await fetch('https://countriesnow.space/api/v0.1/countries/state/cities', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              country: this.locationCountry,
              state: this.locationRegion
            })
          });
          const data = await response.json();
          if (!data.error) {
            if (data.data.length === 0) {
              this.cities = [{ name: 'N/A' }];
            } else {
              this.cities = data.data.map(city => ({
                name: city
              }));
            }
          } else {
            console.error('Failed to fetch cities:', data.msg);
            // Handle error scenario
            
          }
        }
      } catch (error) {
        console.error('Error fetching cities:', error.message);
        // Handle fetch error
      }
    },
  onCountryChange() {
    // Filter states for the selected country
    const selectedCountry = this.countries.find(country => country.name === this.locationCountry);
    this.selectedCountryStates = selectedCountry ? selectedCountry.states : [];
    
    // Reset region and city fields
    this.locationRegion = '';
    this.locationCity = '';
  },

  onRegionChange() {
    this.locationCity = '';

    if (this.locationRegion != "N/A") {
      this.fetchCities();
    } else {
      this.cities = [{ name: 'N/A' }];
    }

  },
  },mounted() {
  // Fetch countries and their states on component mount
  this.fetchCountriesAndStates();
},
};
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.signup {
  max-width: 800px;
  width: 100%;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.signup h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: center;
}

.signup-form {
  display: grid;
  gap: 20px;
}

.form-group {
  display: grid;
  gap: 5px;
  margin-top: 5px;
  margin-bottom: 5px;
}

.input-field {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}

.signup-button {
  background-color: #4b5563;
  color: #ffffff;
  border: none;
  padding: 12px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  width: 100%;
  transition: background-color 0.3s ease;
  margin-top: 5px;
}

.signup-button:hover {
  background-color: #6b7280;
}

.text-red-600 {
  color: #e53e3e;
  font-size: 14px;
  margin-top: 4px;
}

.text-sm {
  font-size: 14px;
}

.location-fields {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.name-fields {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.error-message {
  margin-top: 10px;
}

.error-message ul {
  list-style-type: none;
  padding: 0;
}

.error-message li {
  color: #ff0000;
  font-size: 14px;
  margin-bottom: 5px;
}

@media (max-width: 600px) {
  .signup {
    padding: 10px;
  }
}
</style>
