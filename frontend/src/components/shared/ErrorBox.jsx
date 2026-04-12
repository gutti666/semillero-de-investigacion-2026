export default function ErrorBox({ message }) {
  if (!message) return null
  return (
    <div className="mt-4 bg-[#1a0a0a] border border-[#5a1a1a] rounded-xl px-4 py-3 text-danger text-sm">
      {message}
    </div>
  )
}
