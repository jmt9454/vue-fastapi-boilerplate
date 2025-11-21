<script setup>
import { ref, onMounted } from 'vue'
import { API } from '@/services' // Using the Barrel file

// State
const students = ref([])
const loading = ref(false)
const saving = ref(false) // Loading state for the save button
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
    const res = await API.students.getStudents()
    students.value = res.data
  } catch (error) {
    console.error('Error fetching students', error)
  } finally {
    loading.value = false
  }
}

const save = async () => {
  if (!valid.value) return

  saving.value = true
  try {
    if (editedItem.value.id) {
      // --- UPDATE ---
      await API.students.updateStudent(editedItem.value.id, editedItem.value)
      // Update local state without refreshing API
      const index = students.value.findIndex((s) => s.id === editedItem.value.id)
      if (index !== -1) Object.assign(students.value[index], editedItem.value)
    } else {
      // --- CREATE ---
      const res = await API.students.createStudent(editedItem.value)
      // Add new item to list
      students.value.push(res.data)
    }
    close()
  } catch (e) {
    console.error(e)
  } finally {
    saving.value = false
  }
}

const deleteItemConfirm = async () => {
  saving.value = true
  try {
    await API.students.deleteStudent(editedItem.value.id)
    // Remove from local list
    students.value = students.value.filter((s) => s.id !== editedItem.value.id)
    closeDelete()
  } catch (e) {
    console.error(e)
  } finally {
    saving.value = false
  }
}

// --- Helpers ---

const openCreateDialog = () => {
  editedItem.value = { ...defaultItem }
  dialog.value = true
}

const openEditDialog = (item) => {
  editedItem.value = { ...item }
  dialog.value = true
}

const openDeleteDialog = (item) => {
  editedItem.value = { ...item }
  dialogDelete.value = true
}

const close = () => {
  dialog.value = false
  editedItem.value = { ...defaultItem }
}

const closeDelete = () => {
  dialogDelete.value = false
  editedItem.value = { ...defaultItem }
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

        <v-btn color="white" variant="tonal" prepend-icon="mdi-plus" @click="openCreateDialog">
          New Student
        </v-btn>
      </v-toolbar>

      <v-progress-linear v-if="loading" indeterminate color="blue"></v-progress-linear>

      <v-table>
        <thead>
          <tr>
            <th class="text-left">Name</th>
            <th class="text-left">Major</th>
            <th class="text-left">GPA</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in students" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.major }}</td>
            <td>
              <v-chip :color="item.gpa >= 3.5 ? 'green' : 'orange'" size="small" variant="flat">
                {{ item.gpa || 'N/A' }}
              </v-chip>
            </td>
            <td class="text-right">
              <v-btn
                icon="mdi-pencil"
                size="small"
                variant="text"
                color="blue"
                @click="openEditDialog(item)"
              ></v-btn>
              <v-btn
                icon="mdi-delete"
                size="small"
                variant="text"
                color="red"
                @click="openDeleteDialog(item)"
              ></v-btn>
            </td>
          </tr>
          <tr v-if="!loading && students.length === 0">
            <td colspan="4" class="text-center py-4 text-grey">No students found</td>
          </tr>
        </tbody>
      </v-table>
    </v-card>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editedItem.id ? 'Edit Student' : 'New Student' }}</span>
        </v-card-title>

        <v-card-text>
          <v-form v-model="valid" @submit.prevent="save">
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.name"
                    label="Student Name"
                    :rules="[rules.required]"
                    variant="outlined"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.major"
                    label="Major"
                    :rules="[rules.required]"
                    variant="outlined"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedItem.gpa"
                    label="GPA"
                    type="number"
                    :rules="[rules.gpa]"
                    variant="outlined"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="close">Cancel</v-btn>
          <v-btn color="blue" variant="flat" @click="save" :disabled="!valid" :loading="saving">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogDelete" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Are you sure?</v-card-title>
        <v-card-text>
          This will permanently delete <strong>{{ editedItem.name }}</strong
          >.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="closeDelete">Cancel</v-btn>
          <v-btn color="red" variant="flat" @click="deleteItemConfirm" :loading="saving">
            Delete
          </v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
