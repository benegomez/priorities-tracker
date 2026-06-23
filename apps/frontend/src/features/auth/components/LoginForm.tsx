"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, type LoginFormValues } from "../schemas/login-schema";
import { useLogin } from "../hooks/useLogin";
import type { AuthError } from "../services/auth-service";

export function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);
  const loginMutation = useLogin();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  function onSubmit(data: LoginFormValues) {
    loginMutation.mutate(data);
  }

  function getErrorMessage(): string | null {
    if (!loginMutation.error) return null;
    const err = loginMutation.error as unknown as AuthError;
    if (err.status === 401) return "Credenciales inválidas";
    if (err.status === 403) return "Usuario inactivo. Contacta a tu administrador";
    if (err.status === 429) {
      const seconds = err.retryAfter ?? 60;
      return `Demasiados intentos. Intenta en ${seconds} segundos`;
    }
    return "Error al iniciar sesión";
  }

  const errorMessage = getErrorMessage();

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          autoFocus
          autoComplete="email"
          {...register("email")}
        />
        {errors.email && (
          <span role="alert">{errors.email.message}</span>
        )}
      </div>

      <div>
        <label htmlFor="password">Contraseña</label>
        <div>
          <input
            id="password"
            type={showPassword ? "text" : "password"}
            autoComplete="current-password"
            {...register("password")}
          />
          <button
            type="button"
            aria-label={showPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? "🙈" : "👁"}
          </button>
        </div>
        {errors.password && (
          <span role="alert">{errors.password.message}</span>
        )}
      </div>

      {errorMessage && (
        <div role="alert">{errorMessage}</div>
      )}

      <button type="submit" disabled={loginMutation.isPending}>
        {loginMutation.isPending ? "Iniciando sesión..." : "Iniciar sesión"}
      </button>
    </form>
  );
}
