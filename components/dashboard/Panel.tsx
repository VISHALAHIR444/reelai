"use client";

import { motion } from "framer-motion";
import { ReactNode } from "react";

interface PanelProps {
  title: string;
  subtitle?: string;
  children: ReactNode;
  action?: ReactNode;
  className?: string;
}

export function Panel({ title, subtitle, children, action, className = "" }: PanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      className={`studio-panel studio-panel-hover p-6 ${className}`}
    >
      <div className="flex items-start justify-between mb-6">
        <div className="space-y-1">
          <h3 className="text-lg font-semibold text-studio-paper">{title}</h3>
          {subtitle && (
            <p className="studio-text-label">{subtitle}</p>
          )}
        </div>
        {action && <div>{action}</div>}
      </div>
      <div>{children}</div>
    </motion.div>
  );
}
