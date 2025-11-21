<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

// State
const students = ref([])
const loading = ref(false)
const dialog = ref(false)
const dialogDelete = ref(false)
const valid = ref(false)

// Form State
const defaultItem = {
  name: '',
  major: '',
  gpa: '',
}
const editedItem = ref({ ...defaultItem })
const editedIndex = ref(-1) // -1 means "New Item", 0+ means "Editing Index X"

// Validation Rules
const rules = {
  required: (value) => !!value || 'Required.',
  gpa: (value) => {
    const num = parseFloat(value)
    return (num >= 0 && num <= 4.0) || 'GPA must be between 0 and 4.0'
  },
}

// --- Actions ---

const fetchStudents = async () => {
  loading.value = true
  try {
    const res = await api.getStudents()
    students.value = res.data
  } catch (error) {
    console.error('Error fetching students', error)
  } finally {
    loading.value = false
  }
}

const save = async () => {
  if (!valid.value) return

  if (editedIndex.value > -1) {
    // Update existing
    try {
      await api.updateStudent(editedItem.value.id, editedItem.value)
      Object.assign(students.value[editedIndex.value], editedItem.value)
    } catch (e) {
      console.error(e)
    }
  } else {
    // Create new
    try {
      const res = await api.createStudent(editedItem.value)
      students.value.push(res.data)
    } catch (e) {
      console.error(e)
    }
  }
  close()
}

const deleteItemConfirm = async () => {
  try {
    await api.deleteStudent(editedItem.value.id)
    students.value.splice(editedIndex.value, 1)
  } catch (e) {
    console.error(e)
  }
  closeDelete()
}

// --- Helpers ---

const editItem = (item) => {
  editedIndex.value = students.value.indexOf(item)
  editedItem.value = { ...item }
  dialog.value = true
}

const deleteItem = (item) => {
  editedIndex.value = students.value.indexOf(item)
  editedItem.value = { ...item }
  dialogDelete.value = true
}

const close = () => {
  dialog.value = false
  editedItem.value = { ...defaultItem }
  editedIndex.value = -1
}

const closeDelete = () => {
  dialogDelete.value = false
  editedItem.value = { ...defaultItem }
  editedIndex.value = -1
}

// Initial Load
onMounted(fetchStudents)
</script>

<template>
  <v-container>
    <v-card class="elevation-2">
      <v-toolbar flat color="primary">
        <v-toolbar-title>Student Records</v-toolbar-title>
        <v-spacer></v-spacer>

        <!-- Add Button -->
        <v-btn color="white" variant="tonal" prepend-icon="mdi-plus" @click="dialog = true">
          New Student
        </v-btn>
      </v-toolbar>

      <!-- Data Table -->
      <v-table>
        <thead>
          <tr>
            <th class="text-left">ID</th>
            <th class="text-left">Name</th>
            <th class="text-left">Major</th>
            <th class="text-left">GPA</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in students" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.major }}</td>
            <td>
              <v-chip :color="item.gpa >= 3.5 ? 'green' : 'orange'" size="small">
                {{ item.gpa || 'N/A' }}
              </v-chip>
            </td>
            <td class="text-right">
              <v-icon size="small" class="me-2" @click="editItem(item)" color="blue"
                >mdi-pencil</v-icon
              >
              <v-icon size="small" @click="deleteItem(item)" color="red">mdi-delete</v-icon>
            </td>
          </tr>
          <tr v-if="students.length === 0">
            <td colspan="5" class="text-center py-4 text-grey">No students found</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editedIndex === -1 ? 'New Student' : 'Edit Student' }}</span>
        </v-card-title>

        <v-card-text>
          <v-form v-model="valid">
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.name"
                    label="Student Name"
                    :rules="[rules.required]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.major"
                    label="Major"
                    :rules="[rules.required]"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.gpa"
                    label="GPA"
                    type="number"
                    :rules="[rules.gpa]"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="close">Cancel</v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="save" :disabled="!valid">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="dialogDelete" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Are you sure?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancel</v-btn>
          <v-btn color="red-darken-1" variant="text" @click="deleteItemConfirm">OK</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
