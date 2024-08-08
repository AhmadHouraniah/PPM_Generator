# Partial Product Multiplier (PPM) IP Generator

A Partial Product Multiplier (PPM) computes a multiplication and produces two outputs. By adding these outputs, you obtain the final product. This approach allows for optimizations as the final addition can have a longer critical path.

## Usage

To generate a PPM, use the following command:

```sh
python3 generatePPM.py --M <A Width> --N <B Width> --signed <0/1> --type <wallace/dadda/RoCoCo> --sim <0/1>

--M : Width of input A
--N : Width of input B
--signed : Set to 1 for signed multiplication, 0 for unsigned
--type : Type of multiplier (wallace, dadda, RoCoCo)
--sim : Set to 1 to enable simulation (requires iverilog), 0 to disable
```

## Notes
The PPM type option is not currently supported. This feature will be added in future versions.
Signed multiplications are only supported when N equals M.

## Simulation
If you want to simulate the generated PPM, make sure iverilog is installed on your system. You can install it using:
```sh
sudo apt-get install iverilog
```
