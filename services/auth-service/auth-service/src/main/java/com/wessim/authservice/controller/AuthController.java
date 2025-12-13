package com.wessim.authservice.controller;

import com.wessim.authservice.entity.LoginDTO;
import com.wessim.authservice.entity.RegisterDTO;
import com.wessim.authservice.entity.User;
import com.wessim.authservice.service.AuthService;
import com.wessim.authservice.service.JWTService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {

    @Autowired
    private AuthService authService;
    @Autowired
    private JWTService jwtService;

    @PostMapping("/register")
    public ResponseEntity<Map<String, Object>> register(@RequestBody RegisterDTO dto) {
        User user = authService.register(dto.getUsername(), dto.getEmail(), dto.getPassword(), dto.getRole());

        Map<String, Object> response = new HashMap<>();
        response.put("id", user.getId());
        response.put("username", user.getUsername());
        response.put("email", user.getEmail());

        return ResponseEntity.ok(response);
    }


    @PostMapping("/login")
    public ResponseEntity<Map<String, Object>> login(@RequestBody LoginDTO dto) {

        User user = authService.login(dto.getUsername());

        if (user != null && authService.checkPassword(dto.getPassword(), user.getPasswordHash())) {

            Map<String, Object> extraClaims = new HashMap<>();
            extraClaims.put("role", user.getRole().name());
            extraClaims.put("id", user.getId());
            extraClaims.put("email", user.getEmail());

            UserDetails userDetails = org.springframework.security.core.userdetails.User
                    .withUsername(user.getUsername())
                    .password(user.getPasswordHash())
                    .authorities(user.getRole().name())
                    .build();

            String jwt = jwtService.generateToken(extraClaims, userDetails);

            Map<String, Object> response = new HashMap<>();
            response.put("token", jwt);

            return ResponseEntity.ok(response);
        }

        return ResponseEntity.status(401).body(Map.of("error", "Invalid credentials"));
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<Map<String, Object>> delete(@RequestHeader("Authorization") String token, @PathVariable int id) {
        if (!jwtService.isAdmin(token)) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body(Map.of("error", "Access denied"));
        }
        boolean deleted = authService.deleteUserById(id);

        if (deleted) {
            return ResponseEntity.ok(Map.of("message", "User deleted successfully"));
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of("error", "User not found"));
        }
    }



}

