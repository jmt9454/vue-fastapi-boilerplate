import StudentService from './StudentService'
import SystemService from './SystemService'

// Group them into one object
export const API = {
  students: StudentService,
  system: SystemService,
}
