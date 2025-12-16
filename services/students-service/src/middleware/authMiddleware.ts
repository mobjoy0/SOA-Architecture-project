import { Request, Response, NextFunction } from "express";
import jwt, { JwtPayload } from "jsonwebtoken";

// Use environment variable with fallback (only for development)
const JWT_SECRET = process.env.JWT_SECRET || "klrjklgerjhklbhjkesfjytdfsbhgdfbhjvdnjhdgfjhvbnwdgvbng";

if (!process.env.JWT_SECRET) {
    console.warn("WARNING: JWT_SECRET not set in environment variables. Using default (unsafe for production)");
}

interface CustomJWTPayload extends JwtPayload {
    id: number;
    email: string;
    role: string;
    sub: string;
    iat: number;
    exp: number;
}

declare global {
    namespace Express {
        interface Request {
            user?: CustomJWTPayload;
        }
    }
}

export const authenticateToken = (req: Request, res: Response, next: NextFunction) => {
    try {
        const authHeader = req.headers['authorization'];
        const token = authHeader && authHeader.split(' ')[1];

        if (!token) {
            return res.status(401).json({ message: "Access token required" });
        }

        jwt.verify(token, JWT_SECRET, (err: jwt.VerifyErrors | null, decoded: string | jwt.JwtPayload | undefined) => {
            if (err) {
                return res.status(403).json({ message: "Invalid or expired token" });
            }

            req.user = decoded as CustomJWTPayload;
            next();
        });
    } catch (err: any) {
        console.error(err);
        res.status(500).json({ message: "Authentication error" });
    }
};

export const authorizeRole = (...allowedRoles: string[]) => {
    return (req: Request, res: Response, next: NextFunction) => {
        if (!req.user) {
            return res.status(401).json({ message: "Unauthorized" });
        }

        if (!allowedRoles.includes(req.user.role)) {
            return res.status(403).json({
                message: "Forbidden: Insufficient permissions",
                requiredRole: allowedRoles,
                yourRole: req.user.role
            });
        }

        next();
    };
};

export const authorizeOwnerOrAdmin = (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
        return res.status(401).json({ message: "Unauthorized" });
    }

    const resourceId = parseInt(req.params.id);

    if (req.user.role === "ADMIN" || req.user.id === resourceId) {
        next();
    } else {
        return res.status(403).json({ message: "Forbidden: You can only access your own resources" });
    }
};