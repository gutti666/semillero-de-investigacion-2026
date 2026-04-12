export default function Spinner({ visible = false }) {
  if (!visible) return null
  return (
    <div className="flex justify-center my-8">
      <div className="w-11 h-11 rounded-full border-[3px] border-border border-t-teal animate-spin" />
    </div>
  )
}
