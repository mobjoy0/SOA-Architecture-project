import { Router } from "express";
import {
    getAllStudents,
    getStudentById,
    createStudent,
    updateStudent,
    deleteStudent
} from "../controllers/students.controller";
import {authenticateToken, authorizeRole} from "../middleware/authMiddleware";

const router = Router();

router.use(authenticateToken);
router.use(authorizeRole("ADMIN"));

// CRUD routes
router.get("/", getAllStudents);          // GET /students
router.get("/:id", getStudentById);    // GET /students/1
router.post("/", createStudent);       // POST /students
router.put("/:id", updateStudent);     // PUT /students/1
router.delete("/:id", deleteStudent);  // DELETE /students/1

export default router;
