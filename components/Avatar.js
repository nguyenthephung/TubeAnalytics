'use client'
import { useState } from 'react'
import Image from 'next/image'

export default function Avatar({ src, alt, width = 40, height = 40, className = '' }) {
  const [imageError, setImageError] = useState(false)

  const handleImageError = () => {
    setImageError(true)
  }

  if (imageError || !src) {
    // Fallback avatar
    return (
      <div 
        className={`bg-gray-300 flex items-center justify-center rounded-full flex-shrink-0 ${className}`}
        style={{ width: width, height: height, minWidth: width, minHeight: height }}
      >
        <svg 
          className="text-gray-600"
          width={width * 0.5}
          height={height * 0.5}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={2} 
            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" 
          />
        </svg>
      </div>
    )
  }

  return (
    <div 
      className={`rounded-full flex-shrink-0 overflow-hidden ${className}`}
      style={{ width: width, height: height, minWidth: width, minHeight: height }}
    >
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        className="object-cover w-full h-full"
        onError={handleImageError}
      />
    </div>
  )
}