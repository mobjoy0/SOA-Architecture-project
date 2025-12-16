export type StudentRole = "ETUDIANT";

export interface Student {
    id: number;
    fullname: string;
    email: string;
    age: number;
    role: StudentRole;
    password: string;
    major: string;
    level: number;
}
