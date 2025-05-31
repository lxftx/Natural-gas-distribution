export interface FurnaceData {
  C_k: number
  C_pg: number
  V_pg_total: number
  K_total: number
  P_total: number
  N: number
  V_pg_0: number[]
  V_pg_min: number[]
  V_pg_max: number[]
  K_0: number[]
  e: number[]
  P_0: number[]
  S_0: number[]
  S_min: number[]
  S_max: number[]
  delta_P_pg: number[]
  delta_P_k: number[]
  delta_S_pg: number[]
  delta_S_k: number[]
  delta_S_p: number[]
}


export interface ResultData {
  gas_distribution: number[];
  objective: number;
  status: string;
  sulfur_content: number[];
  total_coke_consumption: number;
  total_gas_consumption: number;
  total_iron_production: number;
}

export interface ModalProps {
  data: | ResultData | { error: string};
  onClose: () => void;
}