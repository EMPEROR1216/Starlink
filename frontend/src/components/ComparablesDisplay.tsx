import { Comparable } from '@/types/Comparable';

interface ComparablesDisplayProps {
  comparables: Comparable[];
}

export default function ComparablesDisplay({ comparables }: ComparablesDisplayProps) {
  if (!comparables || comparables.length === 0) {
    return <p className="mt-8 text-center text-gray-500">No comparable properties found.</p>;
  }

  return (
    <div className="mt-10 w-full">
      <h2 className="text-2xl font-semibold mb-4 text-center">Top 3 Comparable Properties</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {comparables.map((comp, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-4 bg-white shadow-md transition-transform hover:scale-105">
            <h3 className="font-bold text-lg text-blue-700">{comp.address}</h3>
            <p className="text-gray-600">Type: <span className="font-medium text-gray-800">{comp.type}</span></p>
            <p className="text-gray-600">Size: <span className="font-medium text-gray-800">{comp.size.toLocaleString()} sqft</span></p>
            <p className="text-gray-600">Age: <span className="font-medium text-gray-800">{comp.age} years</span></p>
            <div className="mt-2 pt-2 border-t">
              <p className="text-gray-600">Confidence Score: <span className="font-bold text-green-600">{comp.confidenceScore.toFixed(2)}</span></p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}