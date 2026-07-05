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

  function handleFormSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    e.stopPropagation();
    handleSubmit(onSubmit)(e);
  }

  return (
    <form onSubmit={handleFormSubmit} action="javascript:void(0)" noValidate className="space-y-4">
      <div className="space-y-1.5">
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="email"
          type="email"
          autoFocus
          autoComplete="email"
          className="flex h-10 w-full rounded-lg border border-border bg-white px-3 py-2 text-sm placeholder:text-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1"
          placeholder="tu@email.com"
          {...register("email")}
        />
        {errors.email && (
          <span role="alert" className="text-xs text-danger">{errors.email.message}</span>
        )}
      </div>

      <div className="space-y-1.5">
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Contraseña
        </label>
        <div className="relative">
          <input
            id="password"
            type={showPassword ? "text" : "password"}
            autoComplete="current-password"
            className="flex h-10 w-full rounded-lg border border-border bg-white px-3 py-2 pr-10 text-sm placeholder:text-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-1"
            placeholder="••••••••"
            {...register("password")}
          />
          <button
            type="button"
            aria-label={showPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-secondary hover:text-gray-700"
          >
            {showPassword ? "🙈" : "👁"}
          </button>
        </div>
        {errors.password && (
          <span role="alert" className="text-xs text-danger">{errors.password.message}</span>
        )}
      </div>

      {errorMessage && (
        <div role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-danger">
          {errorMessage}
        </div>
      )}

      <button
        type="submit"
        disabled={loginMutation.isPending}
        className="flex h-10 w-full items-center justify-center rounded-lg bg-primary text-sm font-medium text-white hover:bg-primary-dark disabled:opacity-50 transition-colors"
      >
        {loginMutation.isPending ? "Iniciando sesión..." : "Iniciar sesión"}
      </button>
    </form>
  );
}
