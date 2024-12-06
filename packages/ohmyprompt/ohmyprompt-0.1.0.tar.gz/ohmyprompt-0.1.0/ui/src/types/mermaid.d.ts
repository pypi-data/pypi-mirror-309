declare module 'mermaid' {
  const mermaid: {
    initialize: (config: any) => void
    run: () => void
    parse: (text: string) => void
    render: (id: string, text: string) => Promise<{ svg: string }>
  }
  export default mermaid
} 