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
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

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
            String jwt = jwtService.generateToken(user);

            Map<String, Object> response = new HashMap<>();
            response.put("token", jwt);
            response.put("username", user.getUsername());
            response.put("role", user.getRole());

            return ResponseEntity.ok(response);
        }

        Map<String, Object> error = new HashMap<>();
        error.put("error", "Invalid username or password");

        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
    }

}

