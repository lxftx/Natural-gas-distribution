export class AuthError extends Error {
  public status?: number

  constructor(message: string, status?: number) {
    super(message)
    this.name = "AuthError"
    this.status = status
  }
}