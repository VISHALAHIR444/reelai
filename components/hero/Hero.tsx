"use client";

import { motion } from "framer-motion";
import Link from "next/link";

export default function Hero() {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-studio-coal/20 via-studio-black to-studio-black" />
      
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-studio-accent/10 rounded-full blur-3xl animate-drift" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-studio-gold/10 rounded-full blur-3xl animate-drift" style={{ animationDelay: '-10s' }} />
      </div>

      <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          className="space-y-8"
        >
          <h1 className="text-display-lg md:text-display-xl text-studio-paper text-balance">
            Reels Studio
          </h1>
          
          <p className="text-xl md:text-2xl text-studio-mist max-w-2xl mx-auto text-balance leading-relaxed">
            Transform long-form into vertical moments.
            <br />
            Calm precision, confident execution.
          </p>

          <div className="flex items-center justify-center gap-4 pt-6">
            <Link href="/add-video">
              <button className="studio-button-primary text-lg px-8 py-4">
                Begin Pipeline
              </button>
            </Link>
            
            <Link href="/dashboard">
              <button className="studio-button-secondary text-lg px-8 py-4">
                Enter Studio
              </button>
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
