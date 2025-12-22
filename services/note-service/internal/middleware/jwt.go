package middleware

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/golang-jwt/jwt/v5"
	"github.com/joho/godotenv"
)

var jwtSecret []byte

func init() {
	if err := godotenv.Load("../../.env"); err != nil {
		log.Println("No .env file found, using environment variables for jwt")
	}

	jwtSecret = []byte(os.Getenv("jwt.secret"))
	if len(jwtSecret) == 0 {
		log.Fatal("JWT_SECRET not set")
	}
}

type contextKey string

const userContextKey = contextKey("user")

type UserClaims struct {
	ID    int64
	Email string
	Role  string
}

func JWTAuthAdmin(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")
		if authHeader == "" {
			http.Error(w, "Forbidden", http.StatusUnauthorized)
			return
		}

		parts := strings.Split(authHeader, " ")
		if len(parts) != 2 || parts[0] != "Bearer" {
			http.Error(w, "Forbidden", http.StatusUnauthorized)
			return
		}

		tokenStr := parts[1]

		token, err := jwt.Parse(tokenStr, func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
			}
			return jwtSecret, nil
		})

		if err != nil {
			log.Printf("Token parse error: %v", err)
			http.Error(w, "Invalid token", http.StatusUnauthorized)
			return
		}

		if !token.Valid {
			log.Println("Token is not valid")
			http.Error(w, "Invalid token", http.StatusUnauthorized)
			return
		}

		if claims, ok := token.Claims.(jwt.MapClaims); ok {
			role, okRole := claims["role"].(string)
			idFloat, okID := claims["id"].(float64)

			log.Printf("Claims: role=%v, id=%v, email=%v", role, idFloat)

			if !okRole || !okID {
				http.Error(w, "Invalid token claims", http.StatusUnauthorized)
				return
			}

			if role != "ADMIN" {
				http.Error(w, "Forbidden: admin only", http.StatusForbidden)
				return
			}

			user := UserClaims{
				ID:   int64(idFloat),
				Role: role,
			}

			ctx := context.WithValue(r.Context(), userContextKey, user)
			r = r.WithContext(ctx)
			next.ServeHTTP(w, r)
			return
		}

		http.Error(w, "Invalid token", http.StatusUnauthorized)
	})
}

func GetUser(r *http.Request) UserClaims {
	if v := r.Context().Value(userContextKey); v != nil {
		return v.(UserClaims)
	}
	return UserClaims{}
}
