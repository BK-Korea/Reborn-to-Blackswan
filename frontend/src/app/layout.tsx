import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'StockOracle - Invest Like the Masters',
  description: 'Get investment insights from Warren Buffett, Peter Lynch, Charlie Munger and other legendary investors. AI-powered analysis for smarter investing.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}