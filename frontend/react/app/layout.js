import './globals.css'

export const metadata = {
  title: 'AutoAgentHire - AI Job Automation',
  description: 'AI-Powered LinkedIn Job Automation Platform',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}