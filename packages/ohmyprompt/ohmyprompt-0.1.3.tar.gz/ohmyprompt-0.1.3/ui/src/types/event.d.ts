interface ChangeEvent<T = Element> {
  target: T & {
    value: string
    checked?: boolean
  }
} 