import { Request, Response } from "express";
import * as studentService from "../services/studentService";
import { StudentDTO } from "../models/studentDTO";
import * as authService from "../services/auth-api.service";

// Helper function to extract token from request
const getTokenFromRequest = (req: Request): string | undefined => {
    const authHeader = req.headers['authorization'];
    if (!authHeader) return undefined;

    const token = authHeader.split(' ')[1];
    return token ? token.trim() : undefined;
};

//POST CREATE STUDENT
export const createStudent = async (req: Request, res: Response) => {
    try {
        const data: StudentDTO = req.body;
        const token = getTokenFromRequest(req);

        // 1. Create user in auth service and get generated password
        const authUser = await authService.createStudentAPI(data, token);

        // 2. Create student in local DB
        const student = studentService.createStudent({
            id: authUser.id,
            fullname: data.fullname,
            email: data.email,
            age: data.age,
            password: authUser.password!,
            major: data.major,
            level: data.level
        });

        // 3. Return student with password
        res.status(201).json({
            id: student.id,
            fullname: student.fullname,
            email: student.email,
            age: student.age,
            role: student.role,
            password: authUser.password
        });
    } catch (err: any) {
        console.error(err);
        res.status(500).json({ message: err.message });
    }
};

//GET STUDENT
export const getAllStudents = (req: Request, res: Response) => {
    try {
        const students = studentService.getAllStudents();
        res.status(200).json(students);
    } catch (err: any) {
        console.error(err);
        res.status(500).json({ message: err.message });
    }
};

export const getStudentById = (req: Request, res: Response) => {
    try {
        const id = parseInt(req.params.id);
        const student = studentService.getStudentById(id);

        if (!student) {
            return res.status(404).json({ message: "Student not found" });
        }

        res.status(200).json(student);
    } catch (err: any) {
        console.error(err);
        res.status(500).json({ message: err.message });
    }
};

export const deleteStudent = async (req: Request, res: Response) => {
    try {
        const id = parseInt(req.params.id);
        const token = getTokenFromRequest(req);

        // 1. Check if student exists
        const student = studentService.getStudentById(id);
        if (!student) {
            return res.status(404).json({ message: "Student not found" });
        }

        // 2. Delete from auth service first
        await authService.deleteStudentAPI(id, token);

        // 3. Delete from local DB
        studentService.deleteStudent(id);

        res.status(200).json({ message: "Student deleted successfully" });
    } catch (err: any) {
        console.error(err);
        res.status(500).json({ message: err.message });
    }
};

export const updateStudent = async (req: Request, res: Response) => {
    try {
        const id = parseInt(req.params.id);
        const data = req.body;
        const token = getTokenFromRequest(req);

        // 1. Check if student exists
        const existingStudent = studentService.getStudentById(id);
        if (!existingStudent) {
            return res.status(404).json({ message: "Student not found" });
        }

        // 2. Update in auth service if email or fullname changed
        if (data.email || data.fullname) {
            await authService.updateStudentAPI(id, {
                email: data.email,
                fullname: data.fullname
            }, token);
        }

        // 3. Update in local DB
        const updatedStudent = studentService.updateStudent(id, data);

        if (!updatedStudent) {
            return res.status(400).json({ message: "No fields to update" });
        }

        res.status(200).json(updatedStudent);
    } catch (err: any) {
        console.error(err);
        res.status(500).json({ message: err.message });
    }
};