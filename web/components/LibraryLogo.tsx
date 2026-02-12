export function LibraryLogo({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden
    >
      <path
        d="M8 8v32c0 2 2 4 4 4h24c2 0 4-2 4-4V8"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M8 8h32v4H8V8z"
        fill="currentColor"
        opacity="0.4"
      />
      <path
        d="M24 12v28M16 20h16M16 26h12"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}
