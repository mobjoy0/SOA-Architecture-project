import db from "../database/DB";
import { Student } from "../models/student";

export const createStudent = (data: Omit<Student, 'role'>): Student => {
    db.prepare(`
        INSERT INTO students (id, fullname, email, age, major, level, role)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `).run(
        data.id,
        data.fullname,
        data.email,
        data.age,
        data.major,
        data.level,
        "ETUDIANT"
    );

    return {
        id: data.id,
        fullname: data.fullname,
        email: data.email,
        age: data.age,
        major: data.major,
        level: data.level,
        role: "ETUDIANT",
        password: data.password
    };
};


export const getAllStudents = (): Omit<Student, 'password'>[] => {
    const students = db.prepare(`
        SELECT id, fullname, email, age, role, major, level
        FROM students
    `).all() as Omit<Student, 'password'>[];

    return students;
};

export const getStudentById = (id: number): Omit<Student, 'password'> | null => {
    const student = db.prepare(`
        SELECT id, fullname, email, age, role, major, level
        FROM students
        WHERE id = ?
    `).get(id) as Omit<Student, 'password'> | undefined;

    return student || null;
};

export const deleteStudent = (id: number): boolean => {
    const result = db.prepare(`
        DELETE FROM students
        WHERE id = ?
    `).run(id);

    return result.changes > 0;
};

export const updateStudent = (id: number, data: Partial<Omit<Student, 'id' | 'role' | 'password'>>): Student | null => {
    const fields: string[] = [];
    const values: any[] = [];

    if (data.fullname) {
        fields.push('fullname = ?');
        values.push(data.fullname);
    }
    if (data.email) {
        fields.push('email = ?');
        values.push(data.email);
    }
    if (data.age) {
        fields.push('age = ?');
        values.push(data.age);
    }

    if (fields.length === 0) {
        return null;
    }

    values.push(id);

    db.prepare(`
        UPDATE students
        SET ${fields.join(', ')}
        WHERE id = ?
    `).run(...values);

    return getStudentById(id) as Student;
};