<template>
    <div v-if="user" :id="`user-${user.id}`" class="max-w-6xl mx-auto mt-8 mb-8">
        <div class="rounded-md p-3 bg-gray-200">
      <Form @submit="updateUser" v-slot="{ errors }" class="signup-form">
        <div class="form-group">
        <label for="name">Name</label>
        <div class="name-fields">
          
          <div>
          <Field name="firstName" v-model="form.firstName" type="text" placeholder="First Name" required class="input-field"
            :rules="validateFirstName" />
          <ErrorMessage name="firstName" class="text-red-600 text-sm" />
        </div>
        <div>
          <Field name="lastName" v-model="form.lastName" type="text" placeholder="Last Name" required class="input-field"
            :rules="validateLastName" />
          <ErrorMessage name="lastName" class="text-red-600 text-sm" />
        </div>
        </div>
      </div>
       
        <div class="form-group">
          <label for="mobileNumber">Mobile Number</label>
          <Field name="mobileNumber" v-model="form.mobileNumber" type="tel" placeholder="Mobile Number" required
            class="input-field" :rules="validateMobileNumber" />
          <ErrorMessage name="mobileNumber" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label for="birthdate">Birthdate</label>
          <Field name="birthdate" v-model="form.birthdate" type="date" required class="input-field" :rules="validateBirthdate" />
          <ErrorMessage name="birthdate" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
        <label for="gender">Gender</label>
        <Field name="gender" v-model="form.gender" as="select" class="input-field" :rules="validateGender">
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </Field>
        <ErrorMessage name="gender" class="text-red-600 text-sm" />
      </div>

      <div class="form-group">
  <label for="sexualOrientation">Sexual Orientation</label>
  <Field name="sexualOrientation" v-model="form.sexualOrientation" as="select" class="input-field" :rules="validateSexualOrientation">
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
  <Field name="genderInterest" v-model="form.genderInterest" as="select" class="input-field" :rules="validateGenderInterest">
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
              <Field name="locationCountry" v-model="form.locationCountry" as="select" class="input-field" @change="onCountryChange" :rules="validateLocationCountry">
        <option value="">Select Country</option>
        <option v-for="(country, index) in countries" :key="index" :value="country.name">{{ country.name }}</option>
      </Field>
              <ErrorMessage name="locationCountry" class="text-red-600 text-sm" />
            </div>
            <div>
              <Field name="locationRegion" v-model="form.locationRegion" as="select" class="input-field" @change="onRegionChange" :rules="validateLocationRegion">
        <option value="">Select Region/State</option>
        <option v-for="(state, index) in selectedCountryStates" :key="index" :value="state.name">{{ state.name }}</option>
      </Field>

              <ErrorMessage name="locationRegion" class="text-red-600 text-sm" />
            </div>
            <div>
              <Field name="locationCity" v-model="form.locationCity" as="select" class="input-field" :rules="validateLocationCity">
          <option value="">Select City</option>
          <option v-for="(city, index) in cities" :key="index" :value="city.name">{{ city.name }}</option>
        </Field>
            <ErrorMessage name="locationCity" class="text-red-600 text-sm" />
          </div>
          </div>
        </div>
        <div class="form-group">
          <label for="school">School</label>
          <Field name="school" v-model="form.school" type="text" placeholder="School" class="input-field"
            :rules="validateSchool" />
          <ErrorMessage name="school" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label for="bio">Bio</label>
          <Field name="bio" v-model="form.bio"as="textarea" rows="4" placeholder="Bio" class="input-field" :rules="validateBio" />
          <ErrorMessage name="bio" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label for="images">Images</label>
          <Field name="images" v-model="form.images" type="file" multiple @change="handleFileUpload"  :rules="validateImages"/>
          <ErrorMessage name="images" class="text-red-600 text-sm" />
        </div>
        <div class="form-group">
          <label class="block text-sm font-medium text-gray-700">Current Images</label>
          <div v-if="form.existingImages.length > 0" class="flex flex-wrap">
            <div v-for="(imageUrl, index) in form.existingImages" :key="index" class="my-2 w-1/4 relative">
              <img :src="imageUrl" class="image-thumbnail" />
              <button type="button" @click="deleteImage(imageUrl)" class="absolute top-1 right-27 px-2 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 text-xs">
                <span>&times;</span>
              </button>
            </div>
          </div>
          <div v-else>
            <p>No images</p>
          </div>
        </div>
        <div class="flex justify-between mt-4">
          <button @click="goBack(user.id)" type="button" class="button-link">Back to Profile</button>
        <button type="submit" class="button-link">Update</button>
        </div>
      </Form>
    </div>
    </div>
    <div v-else class="max-w-md mx-auto mt-8 text-center">
      Loading user...
    </div>
  </template>
  
  <script>
  import gql from 'graphql-tag';
  import { reactive } from 'vue';
  import { Form, Field, ErrorMessage } from 'vee-validate';
  
  export default {
    name: 'ProfileEdit',
    components: {
      Form,
      Field,
      ErrorMessage
    },
    data() {
      return {
        user: null,
        form: reactive({
            firstName: '',
            lastName: '',
            mobileNumber: '',
            birthdate: '',
            locationCountry: '',
            locationRegion: '',
            locationCity: '',
            images: '',
            bio: '',
            school: '',
            sexualOrientation: '',
            gender: '',
            genderInterest: '',
          images: [], // Track new images to upload
          existingImages: [], // Track existing images fetched from server
        }),
        countries: [],
      selectedCountryStates: [],
      cities: [],
      };
    },
    apollo: {
      user: {
        query: gql`
          query User($id: ID!) {
            user(id: $id) {
              id
              firstName
              lastName
              mobileNumber
              birthdate
              locationCountry
              locationRegion
              locationCity
              images
              bio
              school
              sexualOrientation
              gender
              genderInterest
            }
          }
        `,
        variables() {
          return {
            id: this.$route.params.id,
          };
        },
        update(data) {
            this.user = data.user;
          this.form.firstName = data.user.firstName;
          this.form.lastName = data.user.lastName;
          this.form.mobileNumber = data.user.mobileNumber;
          this.form.birthdate = data.user.birthdate;
          this.form.locationRegion = data.user.locationRegion;
          this.form.locationCity = data.user.locationCity;
          this.form.locationCountry = data.user.locationCountry;
          
          
          this.form.bio = data.user.bio;
          this.form.school = data.user.school;
          this.form.gender = data.user.gender;
          this.form.sexualOrientation = data.user.sexualOrientation;
          this.form.genderInterest = data.user.genderInterest;
          this.form.existingImages = data.user.images;
          return data.user;
        },
        error(error) {
          console.error('Error fetching user:', error);
        },
      },
    },
    methods: {
      updateUser() {
        const formData = new FormData();
        formData.append('id', this.user.id);
        formData.append('firstName', this.form.firstName);
        formData.append('lastName', this.form.lastName);
        formData.append('mobileNumber', this.form.mobileNumber);
        formData.append('birthdate', this.form.birthdate);
        formData.append('gender', this.form.gender);
        formData.append('sexualOrientation', this.form.sexualOrientation);
        formData.append('genderInterest', this.form.genderInterest);
        formData.append('locationCountry', this.form.locationCountry);
        formData.append('locationRegion', this.form.locationRegion);
        formData.append('locationCity', this.form.locationCity);
        formData.append('school', this.form.school);
        formData.append('bio', this.form.bio);
        // Append new images to formData only if they are File objects
        const newImages = this.form.images.filter(image => image instanceof File);
        newImages.forEach(image => {
          formData.append('images[]', image);
        });
  
        this.$apollo.mutate({
          mutation: gql`
            mutation UpdateUser(
              $id: ID!, 
              $firstName: String!,
              $lastName: String!,
              $mobileNumber: String!,
              $birthdate: ISO8601Date!,
              $gender: String!,
              $sexualOrientation: String!,
              $genderInterest: String!,
              $locationCountry: String!,
              $locationRegion: String!,
              $locationCity: String!,
              $school: String!,
              $bio: String!,
              $images: [Upload!], 
              $deletedImages: [String!]) {
              updateUserMutation(input: { 
                id: $id, 
                firstName: $firstName,
                lastName: $lastName,
                mobileNumber: $mobileNumber,
                birthdate: $birthdate,
                gender: $gender,
                sexualOrientation: $sexualOrientation,
                genderInterest: $genderInterest,
                locationCountry: $locationCountry,
                locationRegion: $locationRegion,
                locationCity: $locationCity,
                school: $school,
                bio: $bio,
                images: $images,
                deletedImages: $deletedImages
              }) {
                user {
                    id
                    firstName
                    lastName
                    mobileNumber
                    birthdate
                    locationCountry
                    locationRegion
                    locationCity
                    images
                    bio
                    school
                    sexualOrientation
                    gender
                    genderInterest
                }
                errors
              }
            }
          `,
          variables: {
            id: this.user.id,
            firstName: this.form.firstName,
            lastName: this.form.lastName,
            mobileNumber: this.form.mobileNumber,
            birthdate: this.form.birthdate,
            locationCountry: this.form.locationCountry,
            locationRegion: this.form.locationRegion,
            locationCity: this.form.locationCity,
            bio: this.form.bio,
            school: this.form.school,
            gender: this.form.gender,
            sexualOrientation: this.form.sexualOrientation,
            genderInterest: this.form.genderInterest,
            images: newImages, // Only send images that are not deleted
            deletedImages: this.deletedImages // Pass deleted image URLs to mutation
          },
          update: (cache, { data: { updateUserMutation } }) => {
            if (!updateUserMutation || !updateUserMutation.user) {
        console.error('Update mutation did not return expected data:', updateUserMutation);
        return;
      }

      const { user } = updateUserMutation;

      try {
        // Read the existing list of users from the cache
        const data = cache.readQuery({ query: gql`{ users { id firstName lastName mobileNumber birthdate locationCountry locationRegion locationCity bio school gender sexualOrientation genderInterest } }` });

        if (!data || !data.users) {
          return;
        }

        // Update the specific user in the cache with updated data
        const updatedUsers = data.users.map(p => (p.id === user.id ? user : p));

        // Write updated data back to the cache
        cache.writeQuery({
          query: gql`{ users { id firstName lastName mobileNumber birthdate locationCountry locationRegion locationCity bio school gender sexualOrientation genderInterest } }`,
          data: { users: updatedUsers }
        });
      } catch (error) {
        console.error('Error updating cache:', error);
      }
    },
        }).then(() => {
          // Clear images array after successful update
          this.form.images = [];
  
          this.$router.push({ 
            name: 'Profile', 
            params: { id: this.userId },
            query: { successMessage: 'Successfully edited a user' }
          });
        }).catch(error => {
          console.error('Error updating user:', error.message);
        });
      },
      goBack(userId) {
        this.$router.push({ name: 'Profile', params: { id: userId } });
      },
      handleFileUpload(event) {
        const files = event.target.files;
        // Convert FileList to array and assign to form data
        this.form.images = Array.from(files);
      },
      deleteImage(imageUrl) {
        const index = this.form.existingImages.indexOf(imageUrl);
        if (index !== -1) {
          // Create a new array without the deleted item
          this.form.existingImages = this.form.existingImages.filter((_, idx) => idx !== index);
  
          // Add deleted image URL to deletedImages array
          this.deletedImages.push(imageUrl);
          this.validateImages();
          // Force Vue to update DOM after state change
          this.$nextTick(() => {
            // Optionally log or perform further actions after DOM update
            console.log('Images updated:', this.form.images);
           
          });
        }
      },
      validateFirstName(value) {
      if (!value) {
        return 'First Name is required';
      }

      console.log(value)
      return true;
    },
    validateLastName(value) {
      if (!value) {
        return 'Last Name is required';
      }
      console.log(value)
      return true;
    },
    validateMobileNumber(value) {
      if (!value) {
        return 'Mobile Number is required';
      }
      if (!/^(08|09)[0-9]{9}$/.test(value)) {
        return 'Invalid mobile number format';
      }
      console.log(value)
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
  if ((this.form.images.length + this.form.existingImages.length) === 0) {
    return 'At least one image is required';
  }

  if ((this.form.images.length + this.form.existingImages.length) > 5) {
    return 'A maximum of 5 images can be uploaded'
  }
  return true;
},
handleFileUpload(event) {
      const files = event.target.files;
      this.form.images = Array.from(files);
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
        if (this.form.locationCountry && this.form.locationRegion) {
          const response = await fetch('https://countriesnow.space/api/v0.1/countries/state/cities', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              country: this.form.locationCountry,
              state: this.form.locationRegion
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
    const selectedCountry = this.countries.find(country => country.name === this.form.locationCountry);
    this.selectedCountryStates = selectedCountry ? selectedCountry.states : [];
    
    // Reset region and city fields
    this.form.locationRegion = '';
    this.form.locationCity = '';
  },

  onRegionChange() {
    this.form.locationCity = '';

    if (this.form.locationRegion != "N/A") {
      this.fetchCities();
    } else {
      this.cities = [{ name: 'N/A' }];
    }

  },
  },mounted() {
  // Fetch countries and their states on component mount
  this.fetchCountriesAndStates();
},
    computed: {
      deletedImages() {
        return [];
      },
    }
  };
  </script>
  
  <style scoped>
  .image-thumbnail {
    max-width: 100px; /* Adjust max-width as per your requirement */
    height: auto; /* Maintain aspect ratio */
  }
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

.button-link {
  text-decoration: none;
  color: #4b5563; /* Default text color */
  background-color: white;
  border: 1px solid #4b5563;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.button-link:hover {
  background-color: #4b5563; /* Darker background on hover */
  color: white; /* Text color on hover */
}

@media (max-width: 600px) {
  .signup {
    padding: 10px;
  }
}
  </style>
  